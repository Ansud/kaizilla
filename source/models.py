from pydantic import BaseModel, Field


class ReasoningData(BaseModel):
    quality: list[str]
    image_description_keywords: list[str]


class DescriptionData(BaseModel):
    en: str
    ru: str


class DescriptionByType(BaseModel):
    wiki: DescriptionData
    stock: DescriptionData


class CriticismData(BaseModel):
    improvements: str = Field(default="")
    strengths: str = Field(default="")


class ResponseData(BaseModel):
    reasoning: ReasoningData
    description: DescriptionByType
    keywords: list[str]
    criticism: CriticismData
