import { PageContainer } from '@ant-design/pro-components';
import styles from './index.module.css';
import DemoPie from './components/demoPie';
import DemoBullet from './components/demoBullet';
import DemoDualAxes from './components/demoDualAxes';
import DemoBar from './components/demoBar';
import DemoColumn from './components/demoColumn';

const HomePage = () => {
  return (
    <div className={styles.container}>
      <div className={styles.wrapper}>
        <div className={styles.left}>
          <DemoPie />
        </div>

        <div className={styles.middle}>
          <DemoBullet />
        </div>

        <div className={styles.right}>
          <DemoPie />
        </div>
          
      </div>

      {/* 第二行 */}
      <div className={styles.wrapper}>
        <DemoDualAxes />
      </div>

      {/* 第三行 */}
      <div className={styles.wrapper}>
        <div className={styles.left}>
          <DemoBar />
        </div>

        <div className={styles.right}>
          <DemoColumn />
        </div>
      </div>

    </div>
  );
};

export default HomePage;
