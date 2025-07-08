import React from 'react'

export default function Money(props) {
  function handleChange(e) {
    // 父组件进行修改
    props.transform(e.target.value)
  }
  return (
    <div>
      <fieldset>
        <legend>{props.text}</legend>
        <input type="text" value={props.money} onChange={handleChange} />
      </fieldset>
    </div>
  )
}
