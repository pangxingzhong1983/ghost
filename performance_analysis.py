#!/usr/bin/env python3
# -*- coding: UTF8 -*-
"""
性能分析脚本，用于评估Ghost项目的关键模块性能
"""

import cProfile
import pstats
import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath('.'))

def profile_module(module_name):
    """分析指定模块的性能"""
    print(f"\n=== 分析模块: {module_name} ===")
    
    # 尝试导入模块
    try:
        # 处理多级模块导入
        components = module_name.split('.')
        module = __import__(module_name)
        for comp in components[1:]:
            module = getattr(module, comp)
        print(f"成功导入模块: {module_name}")
        
        # 运行性能分析
        profiler = cProfile.Profile()
        
        # 尝试分析模块导入和初始化过程
        profiler.enable()
        
        # 模拟必要的参数
        class MockClient:
            def is_windows(self):
                return False
            def is_linux(self):
                return False
            def is_darwin(self):
                return True
        
        class MockJob:
            pass
        
        class MockIO:
            pass
        
        # 尝试创建模块实例
        if hasattr(module, 'Browser'):
            print("分析Browser模块...")
            # 这里我们只分析模块的导入和类定义，不创建实例
        elif hasattr(module, 'Persistence'):
            print("分析Persistence模块...")
            # 这里我们只分析模块的导入和类定义，不创建实例
        elif hasattr(module, 'Credcap'):
            print("分析Credcap模块...")
            # 这里我们只分析模块的导入和类定义，不创建实例
        elif hasattr(module, 'PortScan'):
            print("分析PortScan模块...")
            # 这里我们只分析模块的导入和类定义，不创建实例
        
        profiler.disable()
        
        # 输出性能分析结果
        stats = pstats.Stats(profiler)
        stats.sort_stats('cumulative')
        stats.print_stats(10)  # 只显示前10个最耗时的函数
        
    except ImportError as e:
        print(f"导入模块失败: {e}")
    except Exception as e:
        print(f"分析模块时出错: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # 确保性能分析器被禁用
        try:
            profiler.disable()
        except:
            pass

def main():
    """主函数"""
    print("=== Ghost 项目性能分析 ===")
    print(f"Python版本: {sys.version}")
    print(f"当前目录: {os.getcwd()}")
    
    # 分析关键模块
    modules_to_profile = [
        'ghost.modules.browser',
        'ghost.modules.persistence',
        'ghost.modules.credcap',
        'ghost.modules.port_scan'
    ]
    
    for module_name in modules_to_profile:
        profile_module(module_name)

if __name__ == "__main__":
    main()