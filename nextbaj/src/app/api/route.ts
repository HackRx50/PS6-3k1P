import { NextResponse } from 'next/server';

export async function GET() {
    console.log('asdf')

    return NextResponse.json({ message: 'Hello, World!' });
}
