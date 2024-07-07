import react, { useState } from 'react'
import "bootstrap/dist/css/bootstrap.min.css"

import './App.css'
import { BrowserRouter, Route, Routes } from 'react-router-dom'
import HomePage from '../pages/HomePage'
import NavBar from '../components/NavBar'

function App() {
    return (
        <>
            <BrowserRouter>
                <NavBar />
                <Routes>
                    <Route path='/' element={<HomePage />} />
                </Routes>
            </BrowserRouter>
        </>
    )
}

export default App
