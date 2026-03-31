from dataclasses import dataclass
from typing import Any
import requests


@dataclass
class TwResponseJson:
    # 关键修改：不用 __ 开头，改用别名接收
    ResultData: Any
    Result: int
    APICheckFlag: str  # 这里改名！去掉 __
    APIVersion: str
    ErrorSeqNum: int
    StatusCode: int
    ResultCode: int
    ResultMessageCode: int
    LogMessage: str
    ResultMessage: str

    @classmethod
    def from_response(cls, response: requests.Response) -> "TwResponseJson":
        json_data = response.json()

        return cls(
            ResultData=json_data.get("ResultData"),
            Result=json_data.get("Result", 0),

            # 核心修复：手动映射 JSON 的 __APICheckFlag 到类的 APICheckFlag
            APICheckFlag=json_data.get("__APICheckFlag", ""),

            APIVersion=json_data.get("APIVersion", ""),
            ErrorSeqNum=json_data.get("ErrorSeqNum", 0),
            StatusCode=json_data.get("StatusCode", 0),
            ResultCode=json_data.get("ResultCode", 0),
            ResultMessageCode=json_data.get("ResultMessageCode", 0),
            LogMessage=json_data.get("LogMessage", ""),
            ResultMessage=json_data.get("ResultMessage", "")
        )