import React from 'react';

import './block.scss';

const Block = ({item, image, active, handleRunProgress}) => {
    return (
        <div className='block'>
            <div className="block__header">
                <div>{item.name}</div>
            </div>
            <div className="block__main"
                style={{
                    backgroundImage: `url('${image}')`,
                    backgroundRepeat: 'no-repeat',
                    backgroundSize: 'cover'
                }}/>
            <div className="block__footer">
                <button disabled = {active ? 'disabled': ''} onClick={handleRunProgress}>
                    {item.level}
                </button>
            </div>
        </div>
    );
};

export default Block;