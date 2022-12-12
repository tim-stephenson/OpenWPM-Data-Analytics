import {Node, parse} from "acorn";


const inputCode: string = process.argv[2];

const code : string = (`
console.log(parse("1 + 1", {
     ecmaVersion: 2022,
    sourceType: "script"
     }
     ));
`);
// const code : string = (`
// 1 + 2 + 3 + 4
// `);

const result : Node =  parse(code, {
     ecmaVersion: 2022,
    sourceType: "script"
     }
);


console.log(JSON.stringify(result, undefined, 4 ) );




function findFunctions(result : Node) : Node[]{
     const functions = [];

     const children : string[] = [
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
     while(toLookAt.length > 0){
          const curr : Node = toLookAt.pop()!;

          if (curr.type == "CallExpression"){
               functions.push(curr);
          }
          children.forEach( (property) => {
               if (curr.hasOwnProperty(property)) {
                    // @ts-ignore
                    const child: Node | Node[] | null | undefined = curr[property];
                    if (child != null && child != undefined){
                         if(Array.isArray(child)){
                              child.forEach( exp => toLookAt.push(exp) );
                         }
                         else{
                              toLookAt.push(child)
                         }
                    }
               }
          });
     }
     return functions
}

const functions : Node[] = findFunctions(result);

functions.forEach( (func : Node) => {
     console.log("------------------------------------------------------------------------------------------------------------------");
     console.log(JSON.stringify(func, undefined, 4) );
})
