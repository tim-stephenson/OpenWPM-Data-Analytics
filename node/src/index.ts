import acorn from "acorn";

console.log(acorn.parse("1 + 1", {
     ecmaVersion: 2022,
    sourceType: "script"
     }
     ));