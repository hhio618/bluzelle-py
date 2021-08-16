import base64
import hashlib
import json
from typing import Dict, List

import ecdsa
from cosmospy.typing import SyncMode
from google.protobuf import json_format
from google.protobuf.any_pb2 import Any
from google.protobuf.message import Message

from bluzelle.codec.cosmos.base.v1beta1.coin_pb2 import Coin
from bluzelle.codec.cosmos.crypto.secp256k1.keys_pb2 import PubKey
from bluzelle.codec.cosmos.tx.signing.v1beta1.signing_pb2 import SignMode
from bluzelle.codec.cosmos.tx.v1beta1.tx_pb2 import (Fee, ModeInfo, SignerInfo,
                                                     Tx)

from ._sign_mode_handler import SignModeHandler
from ._signature import SignatureV2, SignerData, SingleSignatureData
from ._wallet import DEFAULT_BECH32_HRP, privkey_to_address, privkey_to_pubkey


class Transaction:
    """A bluzelle transaction."""

    def __init__(
        self,
        *,
        privkey: bytes,
        account: Any,
        messages: List[Message],
        sign_mode: SignMode,
        fee: Fee,
        memo: str = "",
        chain_id: str = "",
    ) -> None:
        """
        Args:
          privkey: the input private key to sign the raw transaction.
          account: required to create the signer data.
          messages: input bluzelle messages to be included in the transaction.
          sign_mode: for creating the raw transaction, a :term:`SignModeHandler` with
            the same supported mode should be used to sign this transaction later.
          fee: default fee.
          memo: the memo to be included in the transaction.
          chain_id:  required to create the signer data.
        """
        self._privkey = privkey
        self._account = account
        self._messages = messages
        self._sign_mode = sign_mode
        self._fee = fee
        self._memo = memo
        self._chain_id = chain_id

        # Getting the public key from the private key.
        self._pubkey = privkey_to_pubkey(self._privkey)
        



    def _set_messages(self, serialized_messages: List[Any]) -> None:
        """Pack messages and add them to the raw tx"""
        for m in serialized_messages:
            slot = self._tx.body.messages.add()
            slot.Pack(m, type_url_prefix="")
        return self

    def _set_signatures(self, signatures: List[SignatureV2]):
        """Sets the given signatures as the transaction signatures."""
        signer_infos: List[SignerInfo] = []
        raw_sigs: List[bytes] = []

        for index in range(len(signatures)):
            signature = signatures[index]
            if not isinstance(signature.data, SingleSignatureData):
                raise Exception(f"Signature data not supported: {signature.data}")

            data = signature.data
            if data.signature is not None:
                raw_sigs.append(data.signature)

            single = ModeInfo.Single(mode=data.sign_mode)
            mode_info = ModeInfo(single=single)

            signer_info = SignerInfo()
            signer_info.mode_info.CopyFrom(mode_info)
            signer_info.public_key.Pack(
                PubKey(key=signature.pub_key), type_url_prefix=""
            )

            # Do not include default values as per ADR-027.
            if signature.sequence > 0:
                signer_info.sequence = signature.sequence

            signer_infos.append(signer_info)

        # Set the raw signatures.
        for x in range(len(self._tx.signatures[:])):
            del self._tx.signatures[x]
        self._tx.signatures.extend(raw_sigs)

        # Set the signer infos.
        for x in range(len(self._tx.auth_info.signer_infos[:])):
            del self._tx.auth_info.signer_infos[x]
        self._tx.auth_info.signer_infos.extend(signer_infos)
        return self

    def create(self):
        """Creates a raw transaction.
        
        Args:
          sign_mode: 
        Raises:
          ValueError: gas_limit for the transaction should be a positive number.
        """
        self._tx = Tx()
        self._tx.body.memo = self._memo
        
        # Assigning the fee to the tx.
        self._tx.auth_info.fee.CopyFrom(self._fee)
        
        # Adding the messages to the transaction.
        self._set_messages(self._messages)
        
        # Setting the default fees.
        if self._fee is None:
            self._fee = Fee(gas_limit=200000)
        if self._fee.gas_limit == 0:
            raise ValueError("Invalid fees: Invalid gas amount specified.")

        # For SIGN_MODE_DIRECT, calling SetSignatures calls setSignerInfos on
        # TxBuilder under the hood, and SignerInfos is needed to generate the
        # sign bytes. This is the reason for setting SetSignatures here, with a
        # None signature.
        sig_data = SingleSignatureData(sign_mode=self._sign_mode, signature=None)

        # Set SignatureV2 with empty signatures, to set correct signer infos.
        sig = SignatureV2(
            pub_key=self._pubkey,
            data=sig_data,
            sequence=self._account.sequence,
        )
        self._set_signatures([sig])
        return self


    def sign(
        self,
        sign_mode_handler: SignModeHandler,
    ) -> bytes:
        """Sign the raw transaction.
        
        Args:
          sign_mode_handler: Responsible to calculating sign bytes of the signed
             the transaction.
        
        Raises:
          ValueError: for different sign_mode from the current one that used to 
             create the raw transaction. 
        """

        # Checking sign mode from the sign_mode_handler.
        if self._sign_mode != sign_mode_handler.get_mode():
            raise ValueError("The SignMode for the sign_mode_handler and the \
            raw tx sould be the same!")
        
        # Generate the bytes to be signed.
        signer_data = SignerData(
            chain_id=self._chain_id,
            account_number=self._account.account_number,
            sequence=self._account.sequence,
        )
        bytes_to_sign = sign_mode_handler.get_sign_bytes(
            mode=self._sign_mode,
            data=signer_data,
            tx=self._tx,
        )

        # Sign those bytes.
        sig_bytes = self._sign(bytes_to_sign)

        # Construct the SignatureV2 struct.
        sig_data = SingleSignatureData(
            sign_mode=self._sign_mode,
            signature=sig_bytes,
        )
        sig = SignatureV2(
            pub_key=self._pubkey,
            data=sig_data,
            sequence=self._account.sequence,
        )
        # Replace the signature data in the transaction.
        self._set_signatures([sig])

        # Return the signed transaction.
        return self._tx

    def _sign(self, input_bytes) -> str:
        """Signing the input bytes using the same cosmos blockchain format"""
        privkey = ecdsa.SigningKey.from_string(self._privkey, curve=ecdsa.SECP256k1)
        signature_compact = privkey.sign_deterministic(
            input_bytes,
            hashfunc=hashlib.sha256,
            sigencode=ecdsa.util.sigencode_string_canonize,
        )
        return signature_compact
