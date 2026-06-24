from typing import Iterator
from pathlib import Path
from langchain_core.document_loaders import BaseLoader
from langchain_core.documents import Document

class CustomTextLoader(BaseLoader):
    """BaseLoader를 상속받아 구현한 커스텀 텍스트 문서 로더입니다.
    
    기존 TextLoader 소스코드를 참고하여, 파일 경로와 인코딩 설정을 지원하며
    lazy_load() 제너레이터를 구현하여 대용량 파일도 효율적으로 로드할 수 있도록 합니다.
    """

    def __init__(self, file_path: str | Path, encoding: str | None = "utf-8"):
        """파일 경로와 인코딩 형식을 초기화합니다.
        
        Args:
            file_path: 로드할 텍스트 파일의 경로
            encoding: 파일 인코딩 (기본값: 'utf-8')
        """
        self.file_path = Path(file_path)
        self.encoding = encoding

    def lazy_load(self) -> Iterator[Document]:
        """파일을 한 번에 읽어서 Document 객체로 yield합니다.
        
        대용량 리소스를 처리하거나 제너레이터를 이용한 메모리 절약 시
        lazy_load()를 오버라이드하여 제너레이터 형태로 문서를 반환해야 합니다.
        """
        try:
            with open(self.file_path, encoding=self.encoding) as f:
                text = f.read()
        except Exception as e:
            raise RuntimeError(f"Error loading {self.file_path}") from e

        metadata = {"source": str(self.file_path)}
        yield Document(page_content=text, metadata=metadata)
