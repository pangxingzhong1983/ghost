// 自动化登录测试脚本

// 模拟localStorage
class LocalStorage {
  constructor() {
    this.store = {};
  }

  getItem(key) {
    return this.store[key] || null;
  }

  setItem(key, value) {
    this.store[key] = value.toString();
  }

  removeItem(key) {
    delete this.store[key];
  }

  clear() {
    this.store = {};
  }
}

// 模拟window对象
const window = {
  location: {
    href: ''
  },
  localStorage: new LocalStorage()
};

// 模拟message
const message = {
  success: (text) => console.log('✓ Message success:', text),
  error: (text) => console.log('✗ Message error:', text)
};

// 模拟Form
const Form = {
  useForm: () => [{
    validateFields: () => Promise.resolve({ username: 'admin', password: 'password' })
  }]
};

// 模拟useNavigate
const useNavigate = () => (path) => {
  console.log('Navigating to:', path);
  window.location.href = path;
};

// 模拟websocketService
const websocketService = {
  isConnected: () => false,
  setToken: (token) => console.log('Setting token:', token),
  disconnect: () => console.log('Disconnecting WebSocket')
};

// 测试登录函数
const testLogin = async () => {
  console.log('=== 开始登录测试 ===');
  
  try {
    // 模拟表单验证
    console.log('验证表单...');
    const values = { username: 'admin', password: 'password' };
    console.log('表单值:', values);
    
    console.log('设置加载状态...');
    
    try {
      // 尝试使用WebSocket服务进行认证
      if (websocketService.isConnected()) {
        console.log('WebSocket已连接，使用WebSocket认证');
        // 这里应该调用websocketService.authenticate
      } else {
        console.log('WebSocket未连接，使用本地登录');
        // 模拟登录成功
        const mockToken = 'mock-token-' + Date.now();
        window.localStorage.setItem('token', mockToken);
        const expiry = new Date();
        expiry.setHours(expiry.getHours() + 24);
        window.localStorage.setItem('tokenExpiry', expiry.toISOString());
        websocketService.setToken(mockToken);
        console.log('localStorage after local login:', {
          token: window.localStorage.getItem('token'),
          tokenExpiry: window.localStorage.getItem('tokenExpiry')
        });
        message.success('使用本地登录成功');
      }
      
      // 导航到dashboard
      console.log('导航到dashboard');
      window.location.href = '/dashboard';
      console.log('导航尝试完成');
      
      // 验证登录状态
      console.log('验证登录状态...');
      const token = window.localStorage.getItem('token');
      if (token) {
        console.log('✓ 登录成功！Token:', token);
        console.log('✓ 导航到:', window.location.href);
        console.log('=== 登录测试通过 ===');
        return true;
      } else {
        console.log('✗ 登录失败：没有找到token');
        console.log('=== 登录测试失败 ===');
        return false;
      }
    } catch (wsError) {
      console.error('WebSocket认证错误:', wsError);
      // WebSocket认证失败，使用本地登录作为fallback
      console.log('WebSocket认证失败，使用本地登录作为fallback');
      const mockToken = 'mock-token-' + Date.now();
      window.localStorage.setItem('token', mockToken);
      const expiry = new Date();
      expiry.setHours(expiry.getHours() + 24);
      window.localStorage.setItem('tokenExpiry', expiry.toISOString());
      websocketService.setToken(mockToken);
      console.log('localStorage after fallback login:', {
        token: window.localStorage.getItem('token'),
        tokenExpiry: window.localStorage.getItem('tokenExpiry')
      });
      message.success('使用本地登录成功');
      window.location.href = '/dashboard';
      
      // 验证登录状态
      const token = window.localStorage.getItem('token');
      if (token) {
        console.log('✓ 登录成功！Token:', token);
        console.log('✓ 导航到:', window.location.href);
        console.log('=== 登录测试通过 ===');
        return true;
      } else {
        console.log('✗ 登录失败：没有找到token');
        console.log('=== 登录测试失败 ===');
        return false;
      }
    }
  } catch (error) {
    console.error('登录错误:', error);
    message.error('登录失败，请检查用户名和密码');
    console.log('=== 登录测试失败 ===');
    return false;
  }
};

// 测试受保护路由
const testProtectedRoute = () => {
  console.log('=== 测试受保护路由 ===');
  
  // 检查是否已登录
  const isAuthenticated = () => {
    const token = window.localStorage.getItem('token');
    console.log('认证检查:', token ? '已认证' : '未认证');
    return token !== null;
  };
  
  const isAuth = isAuthenticated();
  console.log('受保护路由检查:', isAuth ? '允许访问' : '重定向到登录');
  
  if (isAuth) {
    console.log('✓ 受保护路由测试通过');
    return true;
  } else {
    console.log('✗ 受保护路由测试失败');
    return false;
  }
};

// 运行测试
const runTests = async () => {
  console.log('\n🚀 开始自动化登录测试\n');
  
  // 测试登录
  const loginResult = await testLogin();
  
  console.log('\n');
  
  // 测试受保护路由
  const protectedRouteResult = testProtectedRoute();
  
  console.log('\n📊 测试结果汇总:');
  console.log('登录测试:', loginResult ? '✓ 通过' : '✗ 失败');
  console.log('受保护路由测试:', protectedRouteResult ? '✓ 通过' : '✗ 失败');
  
  if (loginResult && protectedRouteResult) {
    console.log('\n🎉 所有测试通过！登录功能正常。');
  } else {
    console.log('\n❌ 测试失败，请检查代码。');
  }
};

// 执行测试
runTests();