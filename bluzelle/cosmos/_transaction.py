import base64
from bluzelle.codec.cosmos.tx.signing.v1beta1.signing_pb2 import SignMode
import hashlib
import json
from typing import Dict, List

import ecdsa
from google.protobuf.message import Message
from google.protobuf.any_pb2 import Any
from bluzelle.codec.cosmos.tx.v1beta1.tx_pb2 import Tx, Fee, SignerInfo, ModeInfo
from bluzelle.codec.cosmos.base.v1beta1.coin_pb2 import Coin
from bluzelle.codec.cosmos.crypto.secp256k1.keys_pb2 import PubKey
from google.protobuf import json_format
from ._wallet import DEFAULT_BECH32_HRP, privkey_to_address, privkey_to_pubkey
from cosmospy.typing import SyncMode
from ._signature import SignatureV2, SingleSignatureData, SignerData
from ._sign_mode_handler import SignModeHandler


class Transaction:
    """A bluzelle transaction.

    After initialization, one or more token transfers can be added by
    calling the `add_transfer()` method. Finally, call `get_pushable()`
    to get a signed transaction that can be pushed to the `POST /txs`
    endpoint of the Cosmos REST API.
    """

    def __init__(
        self,
        *,
        privkey: bytes,
        account_num: int,
        sequence: int,
        fee: int,
        gas: int,
        fee_denom: str = "ubnt",
        memo: str = "",
        chain_id: str = "cosmoshub-4",
        hrp: str = DEFAULT_BECH32_HRP,
    ) -> None:
        self._privkey = privkey
        self._account_num = account_num
        self._sequence = sequence
        self._fee = Fee(gas_limit=gas, amount=[Coin(denom=fee_denom, amount=str(int(fee)))])
        self._memo = memo
        self._chain_id = chain_id
        self._hrp = hrp
        self._tx = Tx()
        # set memo
        self._tx.body.memo = self._memo
        # set fee
        self._tx.auth_info.fee.CopyFrom(self._fee)



    def _set_messages(self, serialized_messages: List[Any]) -> None:
        for m in serialized_messages:
            slot = self._tx.body.messages.add()
            slot.Pack(m, type_url_prefix='')
        return self
    
    # Sets the given [signatures] as the transaction signatures.
    def _set_signatures(self, signatures: List[SignatureV2]):
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
            print("&&&&&&&&&&&&&&&&&&&&&&& ",signer_info.public_key)
            signer_info.public_key.Pack(PubKey(key=signature.pub_key), type_url_prefix='')

            # Do not include default values as per ADR-027.
            if signature.sequence > 0:
                signer_info.sequence = signature.sequence
            
            signer_infos.append(signer_info)
        

        # Set the raw signatures.
        # TODO: not sure about this.
        for x in range(len(self._tx.signatures[:])):
           del self._tx.signatures[x] 
        self._tx.signatures.extend(raw_sigs)

        # Set the signer infos.
        for x in range(len(self._tx.auth_info.signer_infos[:])):
            del self._tx.auth_info.signer_infos[x]
        self._tx.auth_info.signer_infos.extend(signer_infos)
        return self

    def sign(self, account, sign_mode: SignMode, sign_mode_handler: SignModeHandler, messages: List[Message]) -> bytes:
        self._set_messages(messages)
        # Set the default fees.
        if self._fee is None:
            self._fee = Fee(gas_limit=200000)
        if self._fee.gas_limit == 0:
            raise Exception('Invalid fees: Invalid gas amount specified.')


        # Get the public key from the account, or generate it if
        #  the chain does not have it yet.
        pub_key = privkey_to_pubkey(self._privkey)
        
        # For SIGN_MODE_DIRECT, calling SetSignatures calls setSignerInfos on
        #  TxBuilder under the hood, and SignerInfos is needed to generate the
        #  sign bytes. This is the reason for setting SetSignatures here, with a
        # None signature.
        sig_data = SingleSignatureData(sign_mode=sign_mode, signature=None)

        # Set SignatureV2 with empty signatures, to set correct signer infos.
        sig = SignatureV2(
            pub_key=pub_key,
            data=sig_data,
            sequence=account.sequence,
        )

        self._set_signatures([sig])
        
        # Generate the bytes to be signed.
        signer_data = SignerData(
            chain_id=self._chain_id,
            account_number=account.account_number,
            sequence=account.sequence,
        )
        bytes_to_sign = sign_mode_handler.get_sign_bytes(
            mode=sign_mode,
            data=signer_data,
            tx=self._tx,
        )

        # Sign those bytes.
        sig_bytes = self._sign(bytes_to_sign)

        # Construct the SignatureV2 struct.
        sig_data = SingleSignatureData(
            sign_mode=sign_mode,
            signature=sig_bytes,
        )
        sig = SignatureV2(
            pub_key=pub_key,
            data=sig_data,
            sequence=account.sequence,
        )
        self._set_signatures([sig])
        # Return the signed transaction.
        return self._tx

    def _sign(self, message_bytes) -> str:
        print("message bytes", list(message_bytes))
        privkey = ecdsa.SigningKey.from_string(self._privkey, curve=ecdsa.SECP256k1)
        signature_compact = privkey.sign_deterministic(
            message_bytes, hashfunc=hashlib.sha256, sigencode=ecdsa.util.sigencode_string_canonize
        )
        return signature_compact


