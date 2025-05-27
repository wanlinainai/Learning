// import Student from "./Student"
// import UserGreeting from "./UserGreeting"
import List from "./List/List"

function App() {
  const fruits = [
    { id: 1, name: 'apple', calories: 95 },
    { id: 2, name: 'orange', calories: 105 },
    { id: 3, name: 'banana', calories: 88 },
    { id: 4, name: 'coconut', calories: 100 },
    { id: 5, name: 'pineapple', calories: 90 }
  ]

    const vegetables = [
    { id: 6, name: 'potatoes', calories: 110 },
    { id: 7, name: 'celery', calories: 23 },
    { id: 8, name: 'carrots', calories: 34 },
    { id: 9, name: 'corn', calories: 45 },
    { id: 10, name: 'broccoli', calories: 180 }
  ]
  return (
    <>
      {/* <Student name="海绵宝宝" age={10} isStudent={true}></Student>
      <Student name="派大星" age={20} isStudent={false}></Student>
      <Student name="李白" age={100} isStudent={false}></Student>
      <Student name="Trump" age={79} isStudent={false}></Student>
      <Student /> */}

      {/* <UserGreeting isLoggedIn={true} username="BroCode"/> */}

      <>
        <List category="Fruits" items={ fruits } />
        <List category="Vegetables" items={ vegetables } />
      </>

    </>
  )
}


export default App
