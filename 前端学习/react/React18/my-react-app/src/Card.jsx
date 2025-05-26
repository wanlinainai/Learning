import profilePic from './assets/磁铁.png'
function Card() {
  return (
    <div className="card">
      <img alt="profile picture" src={profilePic} className='card-img' />
      <h2 className='card-title'> Code
      </h2>
      <p className='card-text'> Super idol 的笑容都没你的甜 </p>
    </div>
  )
}

export default Card