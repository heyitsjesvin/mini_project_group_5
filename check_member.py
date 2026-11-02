"""Quick self-check for one member:  python check_member.py N   (N = 1..5)

Members 1-4 run the pipeline up to their own stage on the real data.
Member 5 runs the complete pipeline.
"""
import sys

from etl.common import MEMBER_MODULES, is_stub, run_stages
from etl import member1_extract_and_structure as member1


def main():
    if len(sys.argv) != 2 or not sys.argv[1].isdigit() or int(sys.argv[1]) not in MEMBER_MODULES:
        print("Usage: python check_member.py N   (N = 1, 2, 3, 4 or 5)")
        return 2
    number = int(sys.argv[1])

    waiting = [n for n in range(1, number + 1) if is_stub(n)]
    if waiting:
        print("NOT READY: these members' files are still placeholders: "
              + ", ".join(f"Member {n}" for n in waiting))
        print("Merge the earlier members' pull requests, run 'git pull origin main', "
              "and copy your own file in.")
        return 1

    if number == 5:
        import pipeline
        pipeline.run_etl_pipeline()
        return 0

    raw = member1.extract()
    df = run_stages(raw, number)
    print(f"\nCHECK OK after Member {number}: {df.shape[0]:,} rows x {df.shape[1]} columns")
    return 0


if __name__ == "__main__":
    sys.exit(main())
