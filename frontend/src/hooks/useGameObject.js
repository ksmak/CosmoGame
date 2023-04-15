import { useMemo } from 'react';

export const useGameObject = (items, type) => {
    const researches = useMemo(() => {
        let arr = [];
        items.forEach(item => {
            let el = {...item};
            if (el.obj_type === type) {
                arr.push(el);
            }
        });
        
        return arr;
    }, [items])

    return researches;
}