import { useState } from "react"

function ListOfCar() {
  const [cars, setCars] = useState([])
  const [carYear, setCarYear] = useState(new Date().getFullYear())
  const [carMake, setCarMake] = useState("")
  const [carModel, setCarModel] = useState("")

  function handleAddCar() {
    const newCar = {
      year: carYear,
      make: carMake,
      model: carModel
    };
    setCars(c => [...c, newCar])
    setCarYear(new Date().getFullYear())
    setCarMake("")
    setCarModel("")
  }

  function handleYearChange(event) {
    setCarYear(Number(event.target.value))
  }

  function handleMakeChange(event) {
    setCarMake(event.target.value)
  }

  function handleModelChange(event) {
    setCarModel(event.target.value)
  }

  function handleRemoveCar(index) {
    setCars(c => c.filter((_, i) => i != index))
  }

  return (
    <div>
      <h2>List of Car Objects</h2>
      <ul>
        {
          cars.map((car, index) => <li key={index} onClick={() => handleRemoveCar(index)}>
            {car.year} {car.make} {car.model}
          </li>)
        }
      </ul>
      <input type="number" onChange={handleYearChange} value={carYear} />
      <input type="text" onChange={handleMakeChange} value={carMake} placeholder="Enter car make" />
      <input type="text" onChange={handleModelChange} value={carModel} placeholder="Enter car model" />
      <button onClick={handleAddCar}>Add Car</button>
    </div>
  )
}

export default ListOfCar