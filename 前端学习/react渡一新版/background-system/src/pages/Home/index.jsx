import { PageContainer } from '@ant-design/pro-components';
import { useModel } from '@umijs/max';
import styles from './index.less';
import DemoPie from './components/demoPie';

const HomePage = () => {
  return (
    <PageContainer ghost>
      <div className={styles.container}>
        <DemoPie />
      </div>
    </PageContainer>
  );
};

export default HomePage;
