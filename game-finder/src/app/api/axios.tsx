// src/app/api/axios.tsx
import axios from 'axios';

export default axios.create({
  baseURL: 'http://localhost:8000',   // <- backend
  headers: { 'Content-Type': 'application/json' },
});
