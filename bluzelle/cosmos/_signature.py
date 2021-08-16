import abc
from typing import List, Sequence

import six
from google.protobuf.internal.well_known_types import Any

from bluzelle.codec.cosmos.tx.signing.v1beta1.signing_pb2 import SignMode


# Adapted from here: https://github.com/Echolon166/bluzelle_dart/blob/main/lib/src/types/cosmos_signature.dart

class SignerData:
    """SignerData is the specific information needed to sign a transaction
    that generally isn't included in the transaction body itself.
    """
    # 
    chain_id: str

    # 
    account_number: int


    sequence: int

    def __init__(self, chain_id: str, account_number: int, sequence: int):
        """Creates a new SignerData object.
        Args:
          chain_id: the chain that this transaction is targeted.
          account_number: the account number of the signer.
          sequence: is the account number of the signer that is used for replay
            protection. This field is only useful for Legacy Amino signing, since
            in SIGN_MODE_DIRECT the account sequence is already in the signer info.
        """
        self.chain_id = chain_id
        self.account_number = account_number
        self.sequence = sequence


class SignatureData(six.with_metaclass(abc.ABCMeta)):
    """ SignatureData represents either a SingleSignatureData or a
    MultiSignatureData.
    It is a convenience type that is easier to use in business logic than
    the encoded protobuf ModeInfo's and raw signatures.
    """
    pass


class SingleSignatureData(SignatureData):
    """SingleSignatureData represents the signature and SignMode of a
    single (non-multisig) signer.
    """
    sign_mode: SignMode
    signature: bytes

    def __init__(self, sign_mode: SignMode, signature: bytes) -> None:
        self.sign_mode = sign_mode
        self.signature = signature



class SignatureV2:
    """SignatureV2 is a convenience type that is easier to use in application
    logic than the protobuf SignerInfo's and raw signature bytes.
    It goes beyond the first sdk.Signature types by supporting sign modes and
    explicitly nested multi-signatures.
    It is intended to be used for both building and verifying signatures. 
    """

    pub_key: Any

    
    data: SignatureData

    sequence: int

    def __init__(self, pub_key: Any, data: SignatureData, sequence: int) -> None:
        """Creates a new SignatureV2 object.
        
        Args:
          pub_key: the public key to use for verifying the signature.
          data: is the actual data of the signature which includes SignMode's and
             the signatures themselves for either single or multi-signatures.
          Sequence: is the sequence of this account. Only populated in
             SIGN_MODE_DIRECT.
        """
        self.pub_key = pub_key
        self.data = data
        self.sequence = sequence
