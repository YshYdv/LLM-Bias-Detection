import React from 'react'
import '../components/Home.css'
import MainSection from '../components/MainSection.jsx'


export default function HomePage() {
    return (
        <div className='home-main'>
            <div className='home-right-section'>
                <MainSection />
            </div>
        </div>
    )
}
