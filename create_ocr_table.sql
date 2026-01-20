CREATE TABLE ImageOCRMetadata (
  ImageName NVARCHAR(100),
  ExtractedText NVARCHAR(MAX),
  Language NVARCHAR(20),
  Confidence FLOAT,
  ProcessedAt DATETIME DEFAULT GETDATE()
);
