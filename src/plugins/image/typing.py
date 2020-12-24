from typing import List, TypedDict


class ReplaceUrl(TypedDict):
    ObjURL: str
    ObjUrl: str
    FromURL: str
    FromUrl: str


class Image(TypedDict):
    adType: str
    hasAspData: str
    thumbURL: str
    middleURL: str
    largeTnImageUrl: str
    hasLarge: int
    hoverURL: str
    pageNum: int
    objURL: str
    fromURL: str
    fromURLHost: str
    currentIndex: str
    width: int
    height: int
    type: str
    is_gif: int
    isCopyright: int
    resourceInfo: None
    strategyAssessment: str
    filesize: str
    bdSrcType: str
    di: str
    pi: str
    # is: str
    imgCollectionWord: str
    replaceUrl: List[ReplaceUrl]
    hasThumbData: str
    bdSetImgNum: int
    partnerId: int
    spn: int
    bdImgnewsDate: str
    fromPageTitle: str
    fromPageTitleEnc: str
    bdSourceName: str
    bdFromPageTitlePrefix: str
    isAspDianjing: int
    token: str
    imgType: str
    cs: str
    os: str
    simid: str
    personalized: str
    simid_info: None
    face_info: None
    xiangshi_info: None
    adPicId: str
    source_type: str
