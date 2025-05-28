import { useState } from "react"

// input textarea select radio
function MyComponent() {
  const [name, setName] = useState("Guest")
  const [quantity, setQuantity] = useState(1)
  const [comment, setComment] = useState("")
  const [payment, setPayment] = useState("")
  const [shipping, setShipping] = useState("Delivery")
  function handleNameChange(event) {
    setName(event.target.value)
  }

  function handleQuantity(event) {
    setQuantity(event.target.value)
  }

  function handleComment(event) {
    setComment(event.target.value)
  }

  function handlePayment(event) {
    setPayment(event.target.value)
  }

  function handleShipping(event) {
    setShipping(event.target.value)
  }
  return (
    <>
      <input type="text" value={name} onChange={handleNameChange} />
      <p>Name: {name}</p>

      <input type="number" value={quantity} onChange={handleQuantity}></input>
      <p>Quantity: {quantity}</p>

      <textarea value={comment} onChange={handleComment} placeholder="Enter delivery instructions"></textarea>
      <p>Comment: {comment}</p>

      <select value={payment} onChange={handlePayment}>
        <option value="">Select an option</option>
        <option value="Visa">Visa</option>
        <option value="Mastercard">Mastercard</option>
        <option value="Giftcard">Giftcard</option>
      </select>
      <p>Payment: {payment}</p>

      <label>
        <input type="radio" value="Pick up" checked={shipping === "pick up"} onChange={handleShipping} />
        Pick up
      </label>

      <label >
        <input type="radio" value="Delivery" checked={shipping === 'Delivery'} onChange={handleShipping} />
        Devilery
      </label>
      <p>Shipping: {shipping}</p>
    </>
  )
}

export default MyComponent