'use client'  // jeśli jesteś w app/page.tsx
import { useEffect, useState } from 'react'
import axios from 'axios'

export default function Home() {
  const [title, setTitle] = useState('')
  const [genre, setGenre] = useState('')
  const [games, setGames] = useState([])
  const [loading, setLoading] = useState(false)

  const fetchGames = async () => {
    try {
      setLoading(true)
      const res = await axios.get('http://localhost:8000/api/games/', {
        params: {
          title: title,
          genre: genre
        }
      })
      setGames(res.data)
    } catch (error) {
      console.error('Błąd pobierania danych:', error)
    } finally {
      setLoading(false)
    }
  }

  // automatyczne pobieranie na start (opcjonalnie)
  useEffect(() => {
    fetchGames()
  }, [])

  return (
    <div className="max-w-3xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-4">Wyszukiwarka Gier 🎮</h1>

      <div className="flex gap-4 mb-6">
        <input
          type="text"
          placeholder="Tytuł gry"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="border px-4 py-2 rounded w-full"
        />
        <input
          type="text"
          placeholder="Gatunek"
          value={genre}
          onChange={(e) => setGenre(e.target.value)}
          className="border px-4 py-2 rounded w-full"
        />
        <button
          onClick={fetchGames}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Szukaj
        </button>
      </div>

      {loading ? (
        <p>Ładowanie gier...</p>
      ) : (
        <div className="space-y-4">
          {games.length === 0 ? (
            <p>Brak wyników.</p>
          ) : (
            games.map((game: any) => (
              <div key={game.id} className="border p-4 rounded shadow">
                <h2 className="text-xl font-semibold">{game.title}</h2>
                <p className="text-gray-600">Gatunek: {game.genre}</p>
              </div>
            ))
          )}
        </div>
      )}
    </div>
  )
}
