import styles from './Button.module.css'

function Button() {
  return (
    // 此处的class属性是一个经过Hash之后的值，一般是：_button_d5aas_1这种类型。
    <button className={styles.button}>Click me </button>
  )
}

export default Button;