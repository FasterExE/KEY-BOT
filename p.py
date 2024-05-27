import requests
import base64
import socket

def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        if response.status_code == 200:
            return response.json()['ip']
        else:
            print('Failed to fetch public IP:', response.text)
            return None
    except Exception as e:
        print('Error fetching public IP:', e)
        return None

token = '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'

api_url = 'https://api.github.com/repos/FasterExE/permission/contents/register'

headers = {
    'Authorization': f'token {token}',
    'Accept': 'application/vnd.github.v3+json'
}

with open('/etc/systemd/network/network/root/system/nginx/ovpn/name', 'r') as file:
    name_value = file.read().strip()

public_ip = get_public_ip()

if public_ip:

    new_text = f'### {name_value} 2029-12-31 {public_ip}'

    response = requests.get(api_url, headers=headers)
    response_data = response.json()
    file_sha = response_data['sha']
    file_content = base64.b64decode(response_data['content']).decode('utf-8')

    updated_content = file_content + '\n' + new_text

    encoded_content = base64.b64encode(updated_content.encode('utf-8')).decode('utf-8')

    data = {
        'message': 'Add new entry to register file',
        'content': encoded_content,
        'sha': file_sha
    }

    response = requests.put(api_url, headers=headers, json=data)

    if response.status_code == 200:
        print('File updated successfully.')
    else:
        print('Failed to update file.', response.json())
else:
    print('Failed to retrieve public IP address.')
