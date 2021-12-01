from django.http import JsonResponse
from django.http import HttpResponse


class PayloadHandler:
    # TODO: Refactor get_return_code_n_message for better and simpler (function/class) design

    @staticmethod
    def get_return_code_n_message(msg=None):
        if not msg:
            return_code = '9999'
            return_message = '失敗'
        elif msg == 'success':
            return_code = '0000'
            return_message = '成功'
        elif 'Login Fail Over 6 times.' in msg:
            return_code = '0005'
            return_message = '嘗試密碼錯誤超過六次，已鎖定帳號'
        elif 'Enter a valid email address.' in msg:
            return_code = '0004'
            return_message = '密碼不得少於6位或大於10位'
        elif 'Password is too short or too long.' in msg:
            return_code = '0003'
            return_message = '帳號不符合電子郵件格式'
        elif 'Unable to log in with provided credentials.' in msg:
            return_code = '0002'
            return_message = '帳號或密碼不符'
        elif 'Must include "user_account" and "password".' in msg or 'This field may not be blank' in msg:
            return_code = '0001'
            return_message = '缺少所需資料'
        elif 'Account Disabled' in msg:
            return_code = '2001'
            return_message = '帳號已停權'
        elif 'Account Access Denied' in msg:
            return_code = '2002'
            return_message = '此帳號無權限登入'
        elif 'Account Locked' in msg:
            return_code = '2003'
            return_message = '帳號已鎖定，嘗試超過五次'
        elif ('building_name_com_project_id' or 'lot_building_id_floor_no') in msg:
            return_code = '1003'
            return_message = '資料已存在'
        elif 'unique' in msg:
            return_code = '1004'
            return_message = '資料已存在'
        elif 'The parking lot is parked.' in msg:
            return_code = '2003'
            return_message = '車位已隸屬於其他屋主'
        elif 'Invalid value in column: ' in msg:
            return_code = '2004'
            msg = msg[len('Invalid value in column: '):]
            return_message = '下列單位因欄位有誤，導致無法上傳:' + msg
        elif 'Invalid house type.' in msg:
            return_code = '2005'
            return_message = '房屋分類格式錯誤，請重新匯出表單上傳'
        elif 'Invalid parking_lot type.' in msg:
            return_code = '2006'
            return_message = '車位分類格式錯誤，請重新匯出表單上傳'
        elif 'Invalid type' in msg:
            return_code = '2007'
            return_message = '分類格式錯誤，請重新匯出表單上傳'
        elif 'object has no attribute' in msg:
            return_code = '2008'
            return_message = '格式錯誤，請重新上傳'
        elif 'Unsupported file extension.' in msg:
            return_code = '2009'
            return_message = '檔案類型錯誤，請確認上傳的檔案為excel檔'
        elif 'Something went wrong with balance flags. ' in msg:
            return_code = '3001'
            return_message = '大類餘額調整旗標不得超過或少於1個'
        elif 'Something went wrong with balance_priority flags.' in msg:
            return_code = '3002'
            return_message = '期別餘額調整旗標不得超過或少於1個'
        elif 'house_pct should equal 100 percent.' in msg:
            return_code = '3003'
            return_message = '住屋比率未達或超過100%'
        elif 'parkinglot_pct should equal 100 percent.' in msg:
            return_code = '3004'
            return_message = '車位比率未達或超過100%'
        elif 'item_pct should equal 100 percent.' in msg:
            return_code = '3005'
            return_message = '大類比率未達或超過100%'
        elif 'phase_pct should equal 100 percent.' in msg:
            return_code = '3006'
            return_message = '期別比率未達或超過100%'
        elif 'The contract_template had been duplicated.' in msg:
            return_code = '3007'
            return_message = '該合約範本已被當為拆款範本'
        elif 'Phase_start should start from 1.' in msg:
            return_code = '3008'
            return_message = '期別須從1開始'
        elif 'Phase_end should bigger than phase_start.' in msg:
            return_code = '3009'
            return_message = '結束期別須大於開始期別'
        elif 'Non-continuous value of phase.' in msg:
            return_code = '3010'
            return_message = '非連續性期別'
        elif 'Unexpected error occurred in phase properties.' in msg:
            return_code = '3011'
            return_message = '結束期別錯誤'
        elif 'Calc_template has been taken.' in msg:
            return_code = '3012'
            return_message = '已有合約使用這個拆款範本，無法刪除'
        elif "It's registered." in msg:
            return_code = '4001'
            return_message = '該簽訂合約已被使用'
        elif "There's an editable Change record is True." in msg:
            return_code = '4002'
            return_message = '該合約仍有變更項目為可編輯狀態'
        elif "param_invest.ratio should equal 100 percent." in msg:
            return_code = '5001'
            return_message = '投資占比總和未達或超過100%'
        elif 'DivisionByZero' in msg or 'division by zero' in msg:
            return_code = '7001'
            return_message = '除數不得為零'
        elif 'Invalid formula.' in msg:
            return_code = '7002'
            return_message = '無效算式'
        elif 'is not defined' in msg:
            return_code = '7003'
            return_message = '變數未定義'
        elif 'Invalid negative number.' in msg:
            return_code = '7004'
            return_message = '無效負數'
        elif 'cellphone' in msg and 'is exist' in msg:
            return_code = '7005'
            return_message = '電話號碼重複'
        else:
            return_code = '9999'
            return_message = msg

        return return_code, return_message

    @staticmethod
    def set_payload(data, return_code, return_message):

        payload = {
            'status_code': JsonResponse.status_code,
            'status_message': "",
            'return_code': return_code,
            'return_message': return_message
        }

        if data:
            payload['data'] = data
        else:
            payload['data'] = []

        return payload

    @staticmethod
    def set_http_response(file, file_name, content_type):
        from django.utils.encoding import escape_uri_path
        http_response = HttpResponse(
            content=file,
            content_type=content_type
        )

        http_response['Content-Disposition'] = "attachment; filename*=utf-8''{}".format(
            escape_uri_path(file_name))
        http_response['Access-Control-Expose-Headers'] = 'Content-Disposition'

        return http_response

    @staticmethod
    def set_file_name(file_name, extension, code_name=None):
        if code_name:
            code_name = code_name + '_'
        else:
            code_name = ''
        return str(code_name) + str(file_name) + '.' + extension
