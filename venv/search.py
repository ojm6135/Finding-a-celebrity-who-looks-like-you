import os
import sys
import requests


# https://developers.naver.com/docs/clova/api/CFR/API_Guide.md

def search_celeb(file_name):
    client_id = "Vo1CDPBIf_yDts73aI5_"
    client_secret = "phEkFGiZyx"
    url = "https://openapi.naver.com/v1/vision/celebrity"
    files = {'image': open(f'{file_name}', 'rb')}
    headers = {'X-Naver-Client-Id': client_id, 'X-Naver-Client-Secret': client_secret}
    response = requests.post(url, files=files, headers=headers)
    rescode = response.status_code
    
    new_response = response.json()
    
    if (rescode == 200):
        cnt_face = new_response['info']['faceCount']
        
        if (cnt_face > 0):  # 정상적으로 처리되었을 때
            celebrity = new_response['faces'][0]['celebrity']['value']
            confidence = new_response['faces'][0]['celebrity']['confidence']
            confidence = round(confidence * 100)
            return (celebrity, confidence)
        
        else:  # 오류는 발생하지 않았지만, 인식된 얼굴이 없을 때
            return ('다른 파일을 업로드해 주세요.', '(인식된 얼굴이 없습니다.)')
        
    else:  # 오류 발생 시 (파일의 형식이 맞지 않을 때 등)
        error_msg = new_response['errorMessage']
        start_idx = error_msg.index('(')
        error_msg = error_msg[start_idx:]
        return ('다른 파일을 업로드해 주세요.', str(error_msg))