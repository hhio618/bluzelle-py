# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: crud/CrudValue.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from bluzelle.codec.crud import lease_pb2 as crud_dot_lease__pb2

DESCRIPTOR = _descriptor.FileDescriptor(
    name="crud/CrudValue.proto",
    package="bluzelle.curium.crud",
    syntax="proto3",
    serialized_options=b"Z'github.com/bluzelle/curium/x/crud/types",
    create_key=_descriptor._internal_create_key,
    serialized_pb=b"\n\x14\x63rud/CrudValue.proto\x12\x14\x62luzelle.curium.crud\x1a\x10\x63rud/lease.proto\"\x94\x01\n\tCrudValue\x12\x0f\n\x07\x63reator\x18\x01 \x01(\t\x12\x0c\n\x04uuid\x18\x02 \x01(\t\x12\x0b\n\x03key\x18\x03 \x01(\t\x12\r\n\x05value\x18\x04 \x01(\x0c\x12*\n\x05lease\x18\x05 \x01(\x0b\x32\x1b.bluzelle.curium.crud.Lease\x12\x0e\n\x06height\x18\x06 \x01(\x03\x12\x10\n\x08metadata\x18\x07 \x01(\x0c\x42)Z'github.com/bluzelle/curium/x/crud/typesb\x06proto3",
    dependencies=[
        crud_dot_lease__pb2.DESCRIPTOR,
    ],
)


_CRUDVALUE = _descriptor.Descriptor(
    name="CrudValue",
    full_name="bluzelle.curium.crud.CrudValue",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name="creator",
            full_name="bluzelle.curium.crud.CrudValue.creator",
            index=0,
            number=1,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"".decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="uuid",
            full_name="bluzelle.curium.crud.CrudValue.uuid",
            index=1,
            number=2,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"".decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="key",
            full_name="bluzelle.curium.crud.CrudValue.key",
            index=2,
            number=3,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"".decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="value",
            full_name="bluzelle.curium.crud.CrudValue.value",
            index=3,
            number=4,
            type=12,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"",
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="lease",
            full_name="bluzelle.curium.crud.CrudValue.lease",
            index=4,
            number=5,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="height",
            full_name="bluzelle.curium.crud.CrudValue.height",
            index=5,
            number=6,
            type=3,
            cpp_type=2,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="metadata",
            full_name="bluzelle.curium.crud.CrudValue.metadata",
            index=6,
            number=7,
            type=12,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"",
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=65,
    serialized_end=213,
)

_CRUDVALUE.fields_by_name["lease"].message_type = crud_dot_lease__pb2._LEASE
DESCRIPTOR.message_types_by_name["CrudValue"] = _CRUDVALUE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

CrudValue = _reflection.GeneratedProtocolMessageType(
    "CrudValue",
    (_message.Message,),
    {
        "DESCRIPTOR": _CRUDVALUE,
        "__module__": "crud.CrudValue_pb2"
        # @@protoc_insertion_point(class_scope:bluzelle.curium.crud.CrudValue)
    },
)
_sym_db.RegisterMessage(CrudValue)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
