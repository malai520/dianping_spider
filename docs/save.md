# 数据存储

## CSV（默认）

`config.ini` 使用 `save_mode = csv` 时，程序把结果写入仓库下的 `output/`：

- `search_res.csv`
- `detail_res.csv`
- `review_res.csv`

文件使用 UTF-8 BOM，便于直接用 Excel 打开。字典、数组等嵌套字段会保存为 JSON 字符串。`output/` 已加入 `.gitignore`。

## MongoDB（可选）

需要 MongoDB 时配置：

```ini
[config]
save_mode = mongo
mongo_path = mongodb://127.0.0.1:27017
```

MongoDB 保存器在第一次写入时才建立连接，并执行 `ping` 检查；连接失败会给出明确错误，不影响 `--help` 和离线测试。

## 安全注意事项

不要把 Cookie、代理密钥、MongoDB 账号密码或其他凭据提交到仓库。默认配置不包含登录态；若站点要求登录，程序会停止并报告，不会自动处理验证。
