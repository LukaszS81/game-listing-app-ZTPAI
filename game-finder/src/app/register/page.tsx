'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { Button, Form, Input, Alert } from 'antd'
import axios from '../api/axios' // Upewnij się, że ścieżka jest poprawna

const Register = () => {
  const router = useRouter()
  const [error, setError] = useState<string>('')

  useEffect(() => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
  }, [])
  
  useEffect(() => {
    const token = localStorage.getItem('access_token')
    if (token) {
      router.push('/')
    } else {
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
    }
  }, [router])

  const onFinish = async (values: { username: string; password: string }) => {
    setError('')
    try {
      await axios.post('/api/register/', values)
      router.push('/login')
    } catch (err: any) {
      setError('Rejestracja nie powiodła się. Upewnij się, że dane są poprawne.')
    }
  }

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100 p-4">
      <div className="bg-white p-8 rounded shadow-md w-full max-w-md">
        <h1 className="text-2xl font-semibold mb-6 text-center">Zarejestruj się</h1>
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
              Zarejestruj się
            </Button>
          </Form.Item>
        </Form>

        <div className="text-center mt-4">
          Masz już konto?{' '}
          <span
            className="text-blue-600 cursor-pointer underline"
            onClick={() => router.push('/login')}
          >
            Zaloguj się
          </span>
        </div>
      </div>
    </div>
  )
}

export default Register
