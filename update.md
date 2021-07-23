## 修改显示方式
由于pwntools有大量数据干扰观察
```bash
./exp 2> /dev/null >/dev/null &
```
## 修改脚本运行方式
由于exp依赖环境不同,在不指定环境
```bash
python2 exp
```
修改为
```bash
./exp
```
`需要在脚本第一行制定运行环境`

## 新增flag统计
每次攻击检测本次攻击状态和总体攻击状态
