#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OnePerson AI Studio Core - 参数替换测试脚本
用于验证模板参数化的可行性
"""

import json
import re
from pathlib import Path

def main():
    print("🧪 开始测试参数替换...")
    print()
    
    # 1. 读取配置
    print("📖 读取配置文件...")
    config_path = Path(".ai-studio-temp/test/boq-config.json")
    if not config_path.exists():
        print(f"❌ 错误: 配置文件不存在: {config_path}")
        return 1
    
    with open(config_path, 'r', encoding='utf-8-sig') as f:
        config = json.load(f)
    
    print(f"   ✅ 配置已加载 ({len(config)} 个参数)")
    print()
    
    # 2. 替换 .cursorrules
    print("🔄 处理 .cursorrules.template...")
    cursorrules_template = Path(".ai-studio-temp/templates/.cursorrules.template")
    cursorrules_output = Path(".ai-studio-temp/test/.cursorrules.test")
    
    if not cursorrules_template.exists():
        print(f"❌ 错误: 模板文件不存在: {cursorrules_template}")
        return 1
    
    with open(cursorrules_template, 'r', encoding='utf-8') as f:
        template = f.read()
    
    # 替换所有参数
    replaced = template
    for key, value in config.items():
        pattern = r'{{\s*' + key + r'\s*}}'
        replaced = re.sub(pattern, value, replaced)
    
    # 检查是否有未替换的参数
    unreplaced_matches = re.findall(r'{{\s*(\w+)\s*}}', replaced)
    if unreplaced_matches:
        print(f"   ⚠️  警告: 发现 {len(unreplaced_matches)} 个未替换的参数:")
        for match in set(unreplaced_matches):
            print(f"      - {{{{{match}}}}}")
    else:
        print("   ✅ 所有参数已替换")
    
    # 保存输出
    with open(cursorrules_output, 'w', encoding='utf-8') as f:
        f.write(replaced)
    
    template_lines = len(template.splitlines())
    output_lines = len(replaced.splitlines())
    print(f"   📊 原始模板: {template_lines} 行 → 替换后: {output_lines} 行")
    print()
    
    # 3. 替换 fe_developer.mdc
    print("🔄 处理 fe_developer.mdc.template...")
    mdc_template = Path(".ai-studio-temp/templates/.cursor/rules/fe_developer.mdc.template")
    mdc_output = Path(".ai-studio-temp/test/fe_developer.mdc.test")
    
    if not mdc_template.exists():
        print(f"❌ 错误: 模板文件不存在: {mdc_template}")
        return 1
    
    with open(mdc_template, 'r', encoding='utf-8') as f:
        mdc_content = f.read()
    
    # 替换所有参数
    mdc_replaced = mdc_content
    for key, value in config.items():
        pattern = r'{{\s*' + key + r'\s*}}'
        mdc_replaced = re.sub(pattern, value, mdc_replaced)
    
    # 检查是否有未替换的参数
    mdc_unreplaced_matches = re.findall(r'{{\s*(\w+)\s*}}', mdc_replaced)
    if mdc_unreplaced_matches:
        print(f"   ⚠️  警告: 发现 {len(mdc_unreplaced_matches)} 个未替换的参数:")
        for match in set(mdc_unreplaced_matches):
            print(f"      - {{{{{match}}}}}")
    else:
        print("   ✅ 所有参数已替换")
    
    # 保存输出
    with open(mdc_output, 'w', encoding='utf-8') as f:
        f.write(mdc_replaced)
    
    mdc_template_lines = len(mdc_content.splitlines())
    mdc_output_lines = len(mdc_replaced.splitlines())
    print(f"   📊 原始模板: {mdc_template_lines} 行 → 替换后: {mdc_output_lines} 行")
    print()
    
    # 4. 总结
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("✅ 参数替换测试完成！")
    print()
    print("📁 生成的测试文件:")
    print("   - .ai-studio-temp/test/.cursorrules.test")
    print("   - .ai-studio-temp/test/fe_developer.mdc.test")
    print()
    print("📝 下一步:")
    print("   1. 对比测试文件和原始文件")
    print("   2. 检查替换后的内容是否语义正确")
    print("   3. 进行 AI 理解测试（替换 .cursorrules 并测试诊断模式）")
    print()
    
    return 0

if __name__ == '__main__':
    exit(main())

