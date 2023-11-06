import vector_models_pb2 as _vector_models_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetEmbeddingRequest(_message.Message):
    __slots__ = ["input_text"]
    INPUT_TEXT_FIELD_NUMBER: _ClassVar[int]
    input_text: str
    def __init__(self, input_text: _Optional[str] = ...) -> None: ...

class GetEmbeddingResponse(_message.Message):
    __slots__ = ["resulting_embedding"]
    RESULTING_EMBEDDING_FIELD_NUMBER: _ClassVar[int]
    resulting_embedding: _vector_models_pb2.Embedding
    def __init__(self, resulting_embedding: _Optional[_Union[_vector_models_pb2.Embedding, _Mapping]] = ...) -> None: ...

class GetSimilarityRequest(_message.Message):
    __slots__ = ["input_embedding"]
    INPUT_EMBEDDING_FIELD_NUMBER: _ClassVar[int]
    input_embedding: _vector_models_pb2.Embedding
    def __init__(self, input_embedding: _Optional[_Union[_vector_models_pb2.Embedding, _Mapping]] = ...) -> None: ...

class GetSimilarityResponse(_message.Message):
    __slots__ = ["matches", "scores"]
    MATCHES_FIELD_NUMBER: _ClassVar[int]
    SCORES_FIELD_NUMBER: _ClassVar[int]
    matches: _containers.RepeatedScalarFieldContainer[str]
    scores: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, matches: _Optional[_Iterable[str]] = ..., scores: _Optional[_Iterable[float]] = ...) -> None: ...

class LoadQueryRequest(_message.Message):
    __slots__ = ["queries", "thresholds"]
    QUERIES_FIELD_NUMBER: _ClassVar[int]
    THRESHOLDS_FIELD_NUMBER: _ClassVar[int]
    queries: _containers.RepeatedScalarFieldContainer[str]
    thresholds: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, queries: _Optional[_Iterable[str]] = ..., thresholds: _Optional[_Iterable[float]] = ...) -> None: ...

class LoadQueryResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...
