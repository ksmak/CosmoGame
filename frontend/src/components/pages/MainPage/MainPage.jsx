import React, { useState, useEffect, useRef } from 'react';

import Modal from '../../UI/modal/Modal';

import './MainPage.css';
import Block from '../../UI/block/Block';
import { useAuth } from '../../../hooks/useAuth';
import { getGameObjects } from '../../../api/api';
import { useGameObject } from '../../../hooks/useGameObject';

const MainPage = () => {
    const TYPE_RESEARCH = 1;

    const {token} = useAuth();

    const [researchModal, setResearchModal] = useState(false)
    const [buildingsModal, setBuildingsModal] = useState(false)
    const [shipsModal, setShipsModal] = useState(false)
    const [errorModal, setErrorModal] = useState(false)

    const [gameObjects, setGameObjects] = useState([]);
    const researches = useGameObject(gameObjects, TYPE_RESEARCH);

    const [researchQueue, setResearcheQueue] = useState([])
    const [errorMsg, setErrorMsg] = useState('')

    const ws = useRef(null)
    
    const handleGameObjects =  () => {
        getGameObjects(token.access)
        .then(response => response.json())
        .then(result => setGameObjects(result))
    }

    const handleRunProgress = (id) => {
        ws.current.send(JSON.stringify({
            message: "progress",
            game_object_id: id,
        }))
    }

    useEffect(() => {
        ws.current = new WebSocket(`ws://0.0.0.0:8000/ws/game/user/${token.username}/?token=${token.access}`)
        ws.current.onopen = (e) => {
            console.log("Connected!")
        }
        ws.current.onclose = (e) => {
            console.log("Disconnected!")
        }
        ws.current.onmessage = (e) => {
            const data = JSON.parse(e.data)
            
            console.log(data);

            if (!data['result']) {
                setErrorMsg(data['message']);
                setErrorModal(true);
            }
            switch (data.type) {
                case "start_progress_result":
                    const item = researches.find((item) => item.id === data['game_object_id']);
                    setResearcheQueue((prev) => [...prev, item]);
                    break;

                case "end_progress_result":
                    setResearcheQueue((prev) => prev.slice(0, -1))
                    handleGameObjects();
                    break;

                default:
                    console.log("Unknown message type!")
                    break
                }
        }
        handleGameObjects();
    }, [])

    return (
        <div>
            <header>
                {token.username}
                {researchQueue}
            </header>
            <h1>Main page</h1>
            <nav>
                <ul>
                    <li onClick={() => setResearchModal(true)}>Research</li>
                    <li onClick={() => setBuildingsModal(true)}>Building</li>
                    <li onClick={() => setShipsModal(true)}>Ships</li>
                </ul>
            </nav>
            <Modal active={researchModal} setActive={setResearchModal}>
                <div className='modal__content__header'>
                    <h3>Researches</h3>
                    <table>
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>Name</th>
                                <th>Time</th>
                                <th>#</th>
                            </tr>
                        </thead>
                        <tbody>    
                        {researchQueue.length
                            ? researchQueue.map((item, index) => {
                                return <tr key={index}>
                                    <td>{index}</td>
                                    <td>{index}</td>
                                    <td>00:00:00</td>
                                    <td><button>Cancel</button></td>
                                </tr>
                            })
                            : <tr></tr>
                        }
                        </tbody>
                    </table>
                </div>
                <div className="modal__content__body">
                    {researches.length
                        ? researches.map((item) => {
                            return <Block 
                                        key={item.id}
                                        item={item}
                                        image='/images/research/mathematics.png'
                                        handleRunProgress={() => handleRunProgress(item.id)}
                                    />
                            })
                        : 'nothing'
                    }
                </div>
            </Modal>
            <Modal active={buildingsModal} setActive={setBuildingsModal}>
                <h1>Buildins</h1>
            </Modal>
            <Modal active={shipsModal} setActive={setShipsModal}>
                <h1>Ships</h1>
            </Modal>
            <Modal active={errorModal} setActive={setErrorModal}>
                <h1>Error</h1>
                <p>{errorMsg}</p>
            </Modal>
        </div>
    );
};

export default MainPage;