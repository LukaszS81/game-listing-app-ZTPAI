'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { Button, Form, Input, Alert } from 'antd'
import axios from '../api/axios' // Upewnij się, że masz poprawny path

const Login = () => {
  const router = useRouter()
  const [error, setError] = useState<string>('')

  useEffect(() => {
    const token = localStorage.getItem('access_token')
    if (token) {
      router.push('/')
    }
  }, [router])

  const onFinish = async (values: { username: string; password: string }) => {
    setError('')
    try {
      const res = await axios.post('/api/token/', values)
      localStorage.setItem('access_token', res.data.access)
      localStorage.setItem('refresh_token', res.data.refresh)
      router.push('/')
    } catch (err: any) {
      setError('Nieprawidłowa nazwa użytkownika lub hasło.')
    }
  }

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100 p-4">
      <div className="bg-white p-8 rounded shadow-md w-full max-w-md">
        <h1 className="text-2xl font-semibold mb-6 text-center">Zaloguj się</h1>
        <Form layout="vertical" onFinish={onFinish}>
          <Form.Item
            label="Nazwa użytkownika"
            name="username"
            rules={[{ required: true, message: 'Wprowadź nazwę użytkownika' }]}
          >
            <Input placeholder="Username" />
          </Form.Item>
          <Form.Item
            label="Hasło"
            name="password"
            rules={[{ required: true, message: 'Wprowadź hasło' }]}
          >
            <Input.Password placeholder="Hasło" />
          </Form.Item>

          {error && <Alert message={error} type="error" showIcon className="mb-4" />}

          <Form.Item>
            <Button type="primary" htmlType="submit" block>
              Zaloguj się
            </Button>
          </Form.Item>
        </Form>

        <div className="text-center mt-4">
          Nie masz jeszcze konta?{' '}
          <span
            className="text-blue-600 cursor-pointer underline"
            onClick={() => router.push('/register')}
          >
            Zarejestruj się
          </span>
        </div>
      </div>
    </div>
  )
}

export default Login
