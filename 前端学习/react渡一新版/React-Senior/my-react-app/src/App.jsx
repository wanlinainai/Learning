import ChildCom1 from './components/ChildCom1';
import ChildCom2 from './components/ChildCom2';
import withMouseMove from './HOC/withMouseMove';

const NewChildCom1 = withMouseMove(ChildCom1);
const NewChildCom2 = withMouseMove(ChildCom2);

function App(props) {

    return (
        <div style={{
            display: 'flex',
            justifyContent: 'space-around',
            width: '850px'
        }}>
            {/* <ChildCom1 /
            <ChildCom2 /> */}
            {/* <MouseMove render={(props) => <ChildCom1 {...props}/>} />
            <MouseMove render={(props) => <ChildCom2 {...props}/>} /> */}

            <NewChildCom1 />
            <NewChildCom2 />
        </div>
    );
}

export default App;