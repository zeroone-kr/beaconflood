## 설명
beacon flood를 통해 조작된 ssid를 띄우는 프로그램이다.

## 요구사항
- Kali Linux에서 테스트 됨
- ipTIME N150UA2
- root 권한으로 실행
- monitor모드로 설정
```
ifconfig <interface> down
iwconfig <interface> mode monitor
ifconfig <interface> up
```
- /etc/NetworkManager/NetworkManager.conf 아래 추가
```
[keyfile]
unmanaged-devices=interface-name:mon*;interface-name:wlan*mon;mac:00:11:22:33:44:55
```
- 위 와 같이 설정하여 Network manager가 특정 interface를 Manage하지 않도록 설정
- 설정 후 ```sudo reboot``` 혹은 ```sudo systemctl restart NetworkManager```

## 사용법
```
beacon-flood.py <interface> <ssid-list-file>
예시) beacon-flood mon0 ssid-list.txt
```
