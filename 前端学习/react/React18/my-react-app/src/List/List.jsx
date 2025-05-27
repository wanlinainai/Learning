import styles from './List.module.css'

function List(props) {
  // const fruits = [
  //   { id: 1, name: 'apple', calories: 95 },
  //   { id: 2, name: 'orange', calories: 105 },
  //   { id: 3, name: 'banana', calories: 88 },
  //   { id: 4, name: 'coconut', calories: 100 },
  //   { id: 5, name: 'pineapple', calories: 90 }
  // ]

  // sort array
  // fruits.sort((a, b) => a.name.localeCompare(b.name))
  // fruits.sort((a, b) => b.name.localeCompare(a.name))
  // fruits.sort((a, b) => a.calories - b.calories); // numeric
  // fruits.sort((a, b) => b.calories - a.calories);

  // const lowCalFruits = fruits.filter(fruit => fruit.calories < 100)
  // const highCalFruits = fruits.filter(fruit => fruit.calories > 100)

  // props
  const category = props.category;
  const itemList = props.items;

  const listItems = itemList.map(item => <li key={item.id}>
    {item.name}&nbsp;
    <b>{item.calories}</b></li>)

  return (<>
    <h3 className={styles.listCategory}>{category}</h3>
    <ol className={styles.listItems}>{listItems}</ol>
  </>)
}

export default List