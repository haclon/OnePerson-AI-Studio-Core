#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OnePerson AI Studio Core - 自动化安装脚本

用法:
    python install.py --preset python-fastapi-vue3 --name "我的项目" --abbr "MyApp"
    python install.py --interactive
"""

import os
import sys
import json
import re
import argparse
from pathlib import Path

def get_script_dir():
    """获取脚本所在目录（仓库根目录/scripts）"""
    return Path(__file__).parent

def get_repo_root():
    """获取仓库根目录"""
    return get_script_dir().parent

def load_preset(preset_name):
    """加载预设配置"""
    repo_root = get_repo_root()
    preset_path = repo_root / "presets" / f"{preset_name}.json"
    
    if not preset_path.exists():
        print(f"❌ 错误: 预设配置不存在: {preset_path}")
        print(f"\n可用的预设配置:")
        presets_dir = repo_root / "presets"
        if presets_dir.exists():
            for preset_file in presets_dir.glob("*.json"):
                print(f"  - {preset_file.stem}")
        sys.exit(1)
    
    with open(preset_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def replace_parameters(content, params):
    """替换模板中的参数"""
    result = content
    for key, value in params.items():
        pattern = r'{{\s*' + key + r'\s*}}'
        result = re.sub(pattern, str(value), result)
    return result

def check_unreplaced(content):
    """检查是否有未替换的参数"""
    matches = re.findall(r'{{\s*(\w+)\s*}}', content)
    return matches

def install_cursorrules(params, target_dir):
    """安装 .cursorrules 文件"""
    repo_root = get_repo_root()
    template_path = repo_root / "templates" / ".cursorrules.template"
    target_path = target_dir / ".cursorrules"
    
    print(f"\n📝 处理 .cursorrules...")
    
    if target_path.exists():
        response = input(f"  ⚠️  目标文件已存在: {target_path}\n  是否覆盖？(y/N): ")
        if response.lower() != 'y':
            print("  ⏭️  跳过")
            return False
    
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()
    
    content = replace_parameters(template, params)
    
    unreplaced = check_unreplaced(content)
    if unreplaced:
        print(f"  ⚠️  警告: 发现 {len(unreplaced)} 个未替换的参数:")
        for param in set(unreplaced):
            print(f"     - {{{{{param}}}}}")
    
    with open(target_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  ✅ 已生成: {target_path}")
    return True

def install_mdc_rules(params, target_dir):
    """安装 .cursor/rules/ 目录下的所有 .mdc 文件"""
    repo_root = get_repo_root()
    template_dir = repo_root / "templates" / ".cursor" / "rules"
    target_rules_dir = target_dir / ".cursor" / "rules"
    
    print(f"\n📁 处理 .cursor/rules/ 文件...")
    
    # 创建目标目录
    target_rules_dir.mkdir(parents=True, exist_ok=True)
    
    # 处理所有 .mdc.template 文件
    mdc_templates = list(template_dir.glob("*.mdc.template"))
    
    if not mdc_templates:
        print("  ⚠️  警告: 未找到 .mdc.template 文件")
        return False
    
    success_count = 0
    for template_path in mdc_templates:
        target_filename = template_path.stem  # 去掉 .template 后缀
        target_path = target_rules_dir / target_filename
        
        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()
        
        content = replace_parameters(template, params)
        
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  ✅ {target_filename}")
        success_count += 1
    
    print(f"\n  ✅ 已生成 {success_count} 个 .mdc 文件")
    return True

def interactive_mode():
    """交互式模式"""
    print("🚀 OnePerson AI Studio Core - 交互式安装")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
    
    # 选择预设
    repo_root = get_repo_root()
    presets_dir = repo_root / "presets"
    presets = [p.stem for p in presets_dir.glob("*.json")]
    
    print("可用的技术栈预设:")
    for i, preset in enumerate(presets, 1):
        print(f"  {i}. {preset}")
    
    preset_choice = input(f"\n请选择 (1-{len(presets)}): ")
    try:
        preset_index = int(preset_choice) - 1
        if 0 <= preset_index < len(presets):
            preset_name = presets[preset_index]
        else:
            print("❌ 无效选择")
            sys.exit(1)
    except ValueError:
        print("❌ 无效输入")
        sys.exit(1)
    
    print(f"\n✅ 选择预设: {preset_name}\n")
    
    # 获取项目信息
    project_name = input("项目名称（全称）: ")
    project_abbr = input("项目缩写（英文，如 MyApp）: ")
    
    # 加载预设
    config = load_preset(preset_name)
    
    # 合并参数
    params = {
        "PROJECT_NAME": project_name,
        "PROJECT_ABBR": project_abbr,
        **config
    }
    
    # 确定目标目录（当前目录）
    target_dir = Path.cwd()
    
    print(f"\n目标目录: {target_dir}")
    response = input("确认安装？(Y/n): ")
    if response.lower() == 'n':
        print("❌ 已取消")
        sys.exit(0)
    
    # 开始安装
    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    install_cursorrules(params, target_dir)
    install_mdc_rules(params, target_dir)
    
    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("🎉 安装完成！")
    print("\n下一步:")
    print("  1. 在 Cursor 中重新加载项目")
    print("  2. 试试诊断模式: ? 我想加个登录功能")
    print("")

def main():
    parser = argparse.ArgumentParser(
        description="OnePerson AI Studio Core 安装脚本"
    )
    parser.add_argument(
        "--preset",
        help="预设配置名称（如 python-fastapi-vue3）"
    )
    parser.add_argument(
        "--name",
        help="项目全称"
    )
    parser.add_argument(
        "--abbr",
        help="项目缩写"
    )
    parser.add_argument(
        "--target",
        help="目标目录（默认为当前目录）",
        default="."
    )
    parser.add_argument(
        "--interactive",
        "-i",
        action="store_true",
        help="交互式模式"
    )
    
    args = parser.parse_args()
    
    # 交互式模式
    if args.interactive or (not args.preset and not args.name):
        interactive_mode()
        return
    
    # 命令行模式
    if not args.preset:
        print("❌ 错误: 请指定 --preset 参数")
        print("用法: python install.py --preset python-fastapi-vue3 --name '我的项目' --abbr 'MyApp'")
        sys.exit(1)
    
    if not args.name or not args.abbr:
        print("❌ 错误: 请指定 --name 和 --abbr 参数")
        sys.exit(1)
    
    # 加载预设
    config = load_preset(args.preset)
    
    # 合并参数
    params = {
        "PROJECT_NAME": args.name,
        "PROJECT_ABBR": args.abbr,
        **config
    }
    
    # 目标目录
    target_dir = Path(args.target).resolve()
    if not target_dir.exists():
        print(f"❌ 错误: 目标目录不存在: {target_dir}")
        sys.exit(1)
    
    print(f"🚀 OnePerson AI Studio Core - 自动安装")
    print(f"目标目录: {target_dir}")
    print(f"预设: {args.preset}")
    print(f"项目: {args.name} ({args.abbr})")
    
    # 开始安装
    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    install_cursorrules(params, target_dir)
    install_mdc_rules(params, target_dir)
    
    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("🎉 安装完成！")
    print("\n下一步:")
    print("  1. 在 Cursor 中重新加载项目")
    print("  2. 试试诊断模式: ? 我想加个登录功能")
    print("")

if __name__ == "__main__":
    main()

