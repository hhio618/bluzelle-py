from typing import List, Sequence,Any

from google.protobuf.message import Message
from bluzelle.codec.cosmos.tx.signing.v1beta1.signing_pb2 import SignMode
from bluzelle.codec.cosmos.tx.v1beta1.tx_pb2 import Tx, SignDoc
from ._signature import SignerData
import abc
import six

# Adapted from here: https://github.com/Echolon166/bluzelle_dart/blob/main/lib/src/types/sign_mode_handler.dart
# SignModeHandler defines a interface to be implemented by types which
#   will handle SignMode's by generating sign bytes from a Tx and
#   SignerData
class SignModeHandler(six.with_metaclass(abc.ABCMeta)):
    # modes is the list of modes supported by this handler.
    modes: List[Any]

    # get_sign_bytes returns the sign bytes for the provided SignMode,
    #   SignerData and Tx, or an error.
    @abc.abstractmethod
    def get_sign_bytes(self, mode: Any, data: SignerData, tx: Tx):
        raise NotImplementedError()

# DirectSignModeHandler defines the [SignMode.SIGN_MODE_DIRECT] SignModeHandler.
class DirectSignModeHandler(SignModeHandler):
    def get_modes(self):
        return [SignMode.SIGN_MODE_DIRECT]

    def get_sign_bytes(self, mode: SignMode, data: SignerData, tx: Tx):
        if mode != SignMode.SIGN_MODE_DIRECT:
            raise Exception('Unsupported sign mode: $mode.');
        

        body_bytes = tx.body.SerializeToString()
        auth_info_bytes = tx.auth_info.SerializeToString()

        sign_doc = SignDoc()
        if body_bytes is not None and len(body_bytes) > 0:
            sign_doc.body_bytes = body_bytes
        

        if auth_info_bytes is not None and len(auth_info_bytes) > 0:
            sign_doc.auth_info_bytes = auth_info_bytes;
        

        if data.chain_id is not None and len(data.chain_id) > 0:
            sign_doc.chain_id = data.chain_id
        

        if data.account_number > 0: 
            sign_doc.account_number = data.account_number
        print("###################### tx auth info", tx.body)
        print("###################### sign_doc auth_info", list(sign_doc.body_bytes))
        return sign_doc.SerializeToString()
