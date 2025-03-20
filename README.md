## 使用说明
### 该文件为在临时虚拟服务器上传文件使用，可以使用http 下载获得，修改自己的api信息，则可上传文件到R2，文件在一次运行后就会自动删除自身。

    将上述代码保存为 r2upload（或 r2upload.py）文件，并确保赋予可执行权限（例如在 Linux/Mac 下运行 chmod +x r2upload）。
    修改代码顶部的配置信息为你自己的 Cloudflare R2 信息。
    上传文件示例：
        不用代理：
```sh
./r2upload example.txt
```
使用代理：
```sh
        ./r2upload -p http://127.0.0.1:8106 example.txt
```
明文的密码信息，所以脚本执行完毕后会自动删除自身，不可重复使用。


