# 同步上游并补译（PowerShell）
#
# 用法：
#   pwsh -File zh/sync_upstream.ps1              # 把上游 main 合进 zh-cn，并重新套用翻译
#   pwsh -File zh/sync_upstream.ps1 -Mirror      # 额外把 upstream-sync 分支硬同步到 upstream/main
#   pwsh -File zh/sync_upstream.ps1 -Push        # 同步成功后把结果推到 origin（只在 origin 上，绝不推 upstream）
#
# 说明：
#   upstream 的 push URL 已被设为 DISABLED，任何 push 都只会到 origin，
#   汉化内容不会进入上游仓库。

param(
    [switch]$Mirror,
    [switch]$Push
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $root

Write-Host "==> 拉取上游 main"
git fetch upstream --tags
$target = (git rev-parse --short upstream/main).Trim()

if ($Mirror) {
    Write-Host "==> 把 upstream-sync 硬同步到 upstream/main ($target)"
    $original = (git rev-parse --abbrev-ref HEAD).Trim()
    git switch upstream-sync
    git reset --hard upstream/main
    git switch $original
}

Write-Host "==> 切换 zh-cn 并合并 upstream/main"
git switch zh-cn
git merge --no-edit upstream/main
if ($LASTEXITCODE -ne 0) {
    Write-Host "合并出现冲突，请手动解决后重新运行本脚本（git status 查看冲突文件）。" -ForegroundColor Yellow
    exit 1
}

Write-Host "==> 重新套用中文翻译"
python zh/apply_translations.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "==> 若有变更则提交"
git add -A
$dirty = (git status --porcelain)
if ($dirty) {
    git commit -m "chore(zh-cn): 同步上游 $target 并补译界面文案"
    Write-Host "已提交。"
}
else {
    Write-Host "无需提交，工作区与上游变更已对齐。"
}

if ($Push) {
    Write-Host "==> 推送到 origin（zh-cn）"
    git push origin zh-cn
}

Write-Host "==> 完成：zh-cn 当前 HEAD = $((git rev-parse --short HEAD).Trim())，上游 = $target"
