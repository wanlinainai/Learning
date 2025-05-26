

function UserGreeting(props) {
  return (
    props.isLoggedIn ? <h2 className="welcome-message">Welcome {props.username}</h2> : <h1 className="login-propmt">Please login to continue</h1>
  )
}

export default UserGreeting