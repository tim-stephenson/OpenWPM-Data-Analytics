import { Node } from "acorn";


export function static_analysis(ast : Node) : boolean {
    const nodes = findASTNodes(ast, {
        "AssignmentExpression" : [],
        "CallExpression" : [],
    });
    nodes["AssignmentExpression"].forEach( (n : Node) => {
        // @ts-ignore
        const left : Node | undefined = n?.left; 
        if(left != undefined && left.type == "MemberExpression"){
            // @ts-ignore
            const property : Node | undefined = left?.property;
            if(property != undefined && property.type == "Identifier" ){
                // @ts-ignore
                switch(property?.name){
                    case "fillStyle":
                        return true;
                }
            }
        }
    } )
    return false;
}

function findASTNodes(result: Node, toLookFor: { [key: string]: [] }) : { [key: string]: Node[] }  {
    const found: { [key: string]: Node[] } = toLookFor;

    const children: string[] = [
        "left",
        "right",
        "body",
        "expression",
        "object",
        "argument",
        "arguments",
        "test",
        "consequent",
        "alternate",
        "block",
        "handler",
        "finalizer",
        "init",
        "update",
        "elements",
        "properties",
        "value",
        "callee",
        "expressions"
    ]

    const toLookAt = [result];
    while (toLookAt.length > 0) {
        const curr: Node = toLookAt.pop()!;
        if (found.hasOwnProperty(curr.type) ){
            found[curr.type].push(curr);
        }
        children.forEach((property) => {
            if (curr.hasOwnProperty(property)) {
                // @ts-ignore
                const child: Node | Node[] | null | undefined = curr[property];
                if (child != null && child != undefined) {
                    if (Array.isArray(child)) {
                        child.forEach(exp => toLookAt.push(exp));
                    }
                    else {
                        toLookAt.push(child)
                    }
                }
            }
        });
    }
    return found;
}