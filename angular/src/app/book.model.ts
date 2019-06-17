export class Book {
    constructor(
        public name: string,
        public type: string,
        public genre: Int8Array,
        public description: string,
        public price: Float64Array,
        public in_stock: Int32Array,
        public last_modified: string,
        public condition: Int8Array
    ) {}
}

/*
export class NewBook extends Book {

}

export class UsedBook extends Book {
    condition: Int8Array;
}
*/