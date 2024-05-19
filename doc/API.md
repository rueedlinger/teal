# teal

> Version 0.1.0

**teal** aims to provide a user-friendly API for working with PDFs which can be easily integrated in an existing
workflow.

## Path Table

| Method | Path                                            | Description                     |
|--------|-------------------------------------------------|---------------------------------|
| POST   | [/convert/libreoffice](#postconvertlibreoffice) | Convert Libreoffice Docs To Pdf |
| POST   | [/convert/pdfa](#postconvertpdfa)               | Convert Pdf To Pdfa With Ocr    |
| POST   | [/pdf/ocr](#postpdfocr)                         | Extract Text With Ocr From Pdf  |
| POST   | [/pdf/table](#postpdftable)                     | Extract Table From Pdf          |
| POST   | [/pdf/text](#postpdftext)                       | Extract Text From Pdf           |

## Reference Table

| Name                                                          | Path                                                                                                                                                                  | Description |
|---------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------|
| Body_convert_libreoffice_docs_to_pdf_convert_libreoffice_post | [#/components/schemas/Body_convert_libreoffice_docs_to_pdf_convert_libreoffice_post](#componentsschemasbody_convert_libreoffice_docs_to_pdf_convert_libreoffice_post) |             |
| Body_convert_pdf_to_pdfa_with_ocr_convert_pdfa_post           | [#/components/schemas/Body_convert_pdf_to_pdfa_with_ocr_convert_pdfa_post](#componentsschemasbody_convert_pdf_to_pdfa_with_ocr_convert_pdfa_post)                     |             |
| Body_extract_table_from_pdf_pdf_table_post                    | [#/components/schemas/Body_extract_table_from_pdf_pdf_table_post](#componentsschemasbody_extract_table_from_pdf_pdf_table_post)                                       |             |
| Body_extract_text_from_pdf_pdf_text_post                      | [#/components/schemas/Body_extract_text_from_pdf_pdf_text_post](#componentsschemasbody_extract_text_from_pdf_pdf_text_post)                                           |             |
| Body_extract_text_with_ocr_from_pdf_pdf_ocr_post              | [#/components/schemas/Body_extract_text_with_ocr_from_pdf_pdf_ocr_post](#componentsschemasbody_extract_text_with_ocr_from_pdf_pdf_ocr_post)                           |             |
| HTTPValidationError                                           | [#/components/schemas/HTTPValidationError](#componentsschemashttpvalidationerror)                                                                                     |             |
| TableExtract                                                  | [#/components/schemas/TableExtract](#componentsschemastableextract)                                                                                                   |             |
| TextExtract                                                   | [#/components/schemas/TextExtract](#componentsschemastextextract)                                                                                                     |             |
| ValidationError                                               | [#/components/schemas/ValidationError](#componentsschemasvalidationerror)                                                                                             |             |

## Path Details

***

### [POST]/convert/libreoffice

- Summary  
  Convert Libreoffice Docs To Pdf

#### RequestBody

- multipart/form-data

```ts
{
  file: string
}
```

#### Responses

- 200 Successful Response

- 422 Validation Error

`application/json`

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

***

### [POST]/convert/pdfa

- Summary  
  Convert Pdf To Pdfa With Ocr

#### RequestBody

- multipart/form-data

```ts
{
  file: string
}
```

#### Responses

- 200 Successful Response

- 422 Validation Error

`application/json`

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

***

### [POST]/pdf/ocr

- Summary  
  Extract Text With Ocr From Pdf

#### RequestBody

- multipart/form-data

```ts
{
  file: string
}
```

#### Responses

- 200 Successful Response

`application/json`

```ts
{
  page: integer
  text: string
}[]
```

- 422 Validation Error

`application/json`

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

***

### [POST]/pdf/table

- Summary  
  Extract Table From Pdf

#### RequestBody

- multipart/form-data

```ts
{
  file: string
}
```

#### Responses

- 200 Successful Response

`application/json`

```ts
{
  page: integer
  index?: integer
  table: {
  }[]
}[]
```

- 422 Validation Error

`application/json`

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

***

### [POST]/pdf/text

- Summary  
  Extract Text From Pdf

#### RequestBody

- multipart/form-data

```ts
{
  file: string
}
```

#### Responses

- 200 Successful Response

`application/json`

```ts
{
  page: integer
  text: string
}[]
```

- 422 Validation Error

`application/json`

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

## References

### #/components/schemas/Body_convert_libreoffice_docs_to_pdf_convert_libreoffice_post

```ts
{
  file: string
}
```

### #/components/schemas/Body_convert_pdf_to_pdfa_with_ocr_convert_pdfa_post

```ts
{
  file: string
}
```

### #/components/schemas/Body_extract_table_from_pdf_pdf_table_post

```ts
{
  file: string
}
```

### #/components/schemas/Body_extract_text_from_pdf_pdf_text_post

```ts
{
  file: string
}
```

### #/components/schemas/Body_extract_text_with_ocr_from_pdf_pdf_ocr_post

```ts
{
  file: string
}
```

### #/components/schemas/HTTPValidationError

```ts
{
  detail: {
    loc?: Partial(string) & Partial(integer)[]
    msg: string
    type: string
  }[]
}
```

### #/components/schemas/TableExtract

```ts
{
  page: integer
  index?: integer
  table: {
  }[]
}
```

### #/components/schemas/TextExtract

```ts
{
  page: integer
  text: string
}
```

### #/components/schemas/ValidationError

```ts
{
  loc?: Partial(string) & Partial(integer)[]
  msg: string
  type: string
}
```
