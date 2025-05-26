import Student from "./Student"

function App() {
  return (
    <>
      <Student name="海绵宝宝" age={10} isStudent={true}></Student>
      <Student name="派大星" age={20} isStudent={false}></Student>
      <Student name="李白" age={100} isStudent={false}></Student>
      <Student name="Trump" age={79} isStudent={false}></Student>
      <Student />
    </>
  )
}


export default App
