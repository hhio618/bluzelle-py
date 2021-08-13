from typing import List, Sequence

from google.protobuf.internal.well_known_types import Any
from bluzelle.codec.cosmos.tx.signing.v1beta1.signing_pb2 import SignMode
import abc
import six

# Adapted from here: https://github.com/Echolon166/bluzelle_dart/blob/main/lib/src/types/cosmos_signature.dart
# [SignerData] is the specific information needed to sign a transaction
#   that generally isn't included in the transaction body itself.
class SignerData:
  # chain_id is the chain that this transaction is targeted.
  chain_id: str

  # account_number is the account number of the signer.
  account_number: int

  # sequence is the account number of the signer that is used for replay
  #   protection. This field is only useful for Legacy Amino signing, since
  #   in SIGN_MODE_DIRECT the account sequence is already in the signer info.
  sequence: int

  def __init__(self, chain_id: str, account_number: int, sequence: int):
      self.chain_id = chain_id
      self.account_number = account_number
      self.sequence = sequence

# SignatureData represents either a SingleSignatureData or a
#   MultiSignatureData.
# It is a convenience type that is easier to use in business logic than
#   the encoded protobuf ModeInfo's and raw signatures.
class SignatureData(six.with_metaclass(abc.ABCMeta)):
    pass

# SingleSignatureData represents the signature and SignMode of a
#   single (non-multisig) signer.
class SingleSignatureData(SignatureData):
    sign_mode: SignMode
    signature: bytes

    def __init__(self, sign_mode: SignMode, signature: bytes) -> None:
        self.sign_mode = sign_mode
        self.signature = signature

# SignatureV2 is a convenience type that is easier to use in application
#   logic than the protobuf SignerInfo's and raw signature bytes.
# It goes beyond the first sdk.Signature types by supporting sign modes and
#   explicitly nested multi-signatures.
# It is intended to be used for both building and verifying signatures.
class SignatureV2:
    # pub_key is the public key to use for verifying the signature.
    pub_key: Any

    # Data is the actual data of the signature which includes SignMode's and
    #   the signatures themselves for either single or multi-signatures.
    data: SignatureData

    # Sequence is the sequence of this account. Only populated in
    #   SIGN_MODE_DIRECT.
    sequence: int

    def __init__(self, pub_key: Any, data: SignatureData, sequence: int) -> None:
        self.pub_key = pub_key
        self.data = data
        self.sequence = sequence
