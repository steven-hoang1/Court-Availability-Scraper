import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import styles from './App.module.css';

function App() {
  const [count, setCount] = useState(0)

  return (
    <h1 className={styles.title}>Hello Tennis World 🎾</h1>
  )
}

export default App
