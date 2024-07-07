import React from 'react'
import logo from '../media/logo.png'
import { Link } from 'react-router-dom'

export default function NavBar() {
    return (
        <div className='navbar'>
            <div className='navbar-logo'>
                <img src={logo} alt="" height='30px' className='left-bar-logo'/>
            </div>

            <ul className='navbar-list'>
                <li className='navbar-list-item'>
                    <Link className='navbar-link' to={'/'}>Home</Link>    
                </li>
                <li className='navbar-list-item'>
                    <Link className='navbar-link'>Contact</Link>
                </li>
            </ul>
        </div>
    )
}
