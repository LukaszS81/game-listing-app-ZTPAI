'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { Form, Input, Button, message } from 'antd'
import axios from '../api/axios'

const AddGamePage: React.FC = () => {
  const router = useRouter()
  const [loading, setLoading] = useState(false)

  const onFinish = async (values: any) => {
    setLoading(true)
    const token = localStorage.getItem('access_token')

    try {
      const res = await axios.post(
        '/games/create/',
        values,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      )
      message.success('Gra została dodana!')
      router.push('/') // Po dodaniu wróć na stronę główną
    } catch (err) {
      console.error('Błąd dodawania gry:', err)
      message.error('Nie udało się dodać gry.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-4 bg-gray-100">
      <div className="bg-white p-8 rounded shadow-md w-full max-w-md">
        <h1 className="text-2xl font-semibold mb-6 text-center">Dodaj nową grę</h1>

        <Form layout="vertical" onFinish={onFinish}>
          <Form.Item
            label="Tytuł gry"
            name="title"
            rules={[{ required: true, message: 'Wprowadź tytuł gry' }]}
          >
            <Input />
          </Form.Item>

          <Form.Item
            label="Gatunek"
            name="genre"
            rules={[{ required: true, message: 'Wprowadź gatunek gry' }]}
          >
            <Input />
          </Form.Item>

          <Form.Item label="Opis" name="description">
            <Input.TextArea rows={4} />
          </Form.Item>

          <Form.Item label="URL obrazka" name="img">
            <Input />
          </Form.Item>

          <Form.Item>
            <Button type="primary" htmlType="submit" loading={loading} block>
              Dodaj grę
            </Button>
          </Form.Item>
        </Form>

        <Button type="link" onClick={() => router.push('/')}>
          Anuluj i wróć
        </Button>
      </div>
    </div>
  )
}

export default AddGamePage
