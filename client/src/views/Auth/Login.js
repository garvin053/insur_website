import React from 'react';
import { Link } from 'react-router-dom';

const Login = () => {
  return (
    <div className='container'>
      <h1>Login</h1>
      <form>
        <div className='form-group'>
          <label for='email'>Email Address</label>
          <input
            type='email'
            className='form-control'
            id='email'
            aria-describedby='emailHelp'
            placeholder='Enter a valid and registered email address'
            required
          />
        </div>
        <div className='form-group'>
          <label for='exampleInputPassword1'>Password</label>
          <input
            type='password'
            className='form-control'
            id='exampleInputPassword1'
            placeholder='Password'
          />
        </div>
        <button type='submit' className='btn btn-primary'>
          Login
        </button>
        <Link to='/signup' className='btn btn-link'>
          Signup instead
        </Link>
      </form>
    </div>
  );
};

export default Login;
